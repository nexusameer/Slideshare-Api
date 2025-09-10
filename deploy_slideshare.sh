cat deploy.sh 
#!/bin/bash

echo "=== Slideshare Deployment Script ==="
echo "Starting deployment process..."

# Load environment variables from ~/.bashrc
source ~/.bashrc

# Function to stop and remove containers using port 8000
cleanup_port_8000() {
    echo "Checking for containers using port 8000..."

    # Find containers using port 8000 (both by name and port mapping)
    port_containers=$(docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep ":8000->" | awk '{print $1}')
    slideshare_containers=$(docker ps -aq --filter "name=slideshare")
    
    # Combine and deduplicate container IDs
    all_containers=$(echo -e "$port_containers\n$slideshare_containers" | sort -u | grep -v '^$')
    
    if [ -n "$all_containers" ]; then
        echo "Found containers to stop:"
        docker ps --filter "id=$(echo $all_containers | tr ' ' '\n' | head -1)" --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Status}}"
        
        echo "Stopping and removing existing containers..."
        for container in $all_containers; do
            echo "Stopping container: $container"
            docker stop "$container" 2>/dev/null || true
            echo "Removing container: $container"
            docker rm "$container" 2>/dev/null || true
        done
        echo "✅ Old containers cleaned up"
    else
    echo "No existing containers found using port 8000"
    fi
}

# Function to cleanup old slideshare images only
cleanup_old_images() {
    echo "Cleaning up old slideshare images..."

    # Remove dangling images (untagged)
    dangling=$(docker images -f "dangling=true" -q)
    if [ -n "$dangling" ]; then
        echo "Removing dangling images..."
        docker rmi $dangling 2>/dev/null || true
    fi

    # Keep only the latest 2 versions of nexusameer/slideshare (any tag)
    old_slideshare_images=$(docker images nexusameer/slideshare --format "{{.ID}}" | tail -n +3)
    if [ -n "$old_slideshare_images" ]; then
        echo "Removing old slideshare images..."
        docker rmi $old_slideshare_images 2>/dev/null || true
    fi

    echo "✅ Slideshare image cleanup completed"
}

# Function to show disk usage
show_disk_usage() {
    echo "=== Docker Disk Usage ==="
    docker system df
    echo ""
}

# Main deployment process
main() {
    echo "Starting deployment at $(date)"
    
    # Show initial disk usage
    show_disk_usage
    
    # Cleanup existing containers
    cleanup_port_8000
    
    # Pull optimized image
    echo "Pulling optimized image..."
    docker pull nexusameer/slideshare:optimized

    if [ $? -ne 0 ]; then
        echo "❌ Failed to pull optimized image"
        exit 1
    fi
    echo "✅ Optimized image pulled successfully"

    # Run the new container
    echo "Starting new container..."
    docker run -d --restart always -p 8000:8000 \
      --name slideshare \
      nexusameer/slideshare:optimized
    
    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully"
        
        # Wait a moment for container to initialize
        sleep 5
        
        # Check if container is running
        if docker ps | grep -q "slideshare"; then
            echo "✅ Container is running and healthy"
            
            # Cleanup old images after successful deployment
            cleanup_old_images
            
            # Show final status
            echo ""
            echo "=== Deployment Status ==="
            docker ps --filter "name=slideshare" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            echo ""
            echo "🚀 Deployment completed successfully!"
            echo "Website should be accessible at: http://your-server:8000"
            
        else
            echo "❌ Container failed to start properly"
            echo "Container logs:"
            docker logs slideshare
            exit 1
        fi
    else
        echo "❌ Failed to start container"
        exit 1
    fi
    
    # Show final disk usage
    show_disk_usage
}

# Handle script interruption
trap 'echo "Deployment interrupted"; exit 1' INT TERM

# Run main function
main

echo "Deployment completed at $(date)"