# Download team member images
1..4 | ForEach-Object {
    $url = "https://picsum.photos/400/400"
    $outputPath = "Some web/assets/images/team/team$_.jpg"
    Invoke-WebRequest -Uri $url -OutFile $outputPath
    Start-Sleep -Seconds 1  # Add delay to avoid rate limiting
}

# Download testimonial images
1..6 | ForEach-Object {
    $url = "https://picsum.photos/100/100"
    $outputPath = "Some web/assets/images/testimonials/testimonial$_.jpg"
    Invoke-WebRequest -Uri $url -OutFile $outputPath
    Start-Sleep -Seconds 1  # Add delay to avoid rate limiting
}

# Download portfolio images
1..6 | ForEach-Object {
    $url = "https://picsum.photos/800/600"
    $outputPath = "Some web/assets/images/portfolio/project$_.jpg"
    Invoke-WebRequest -Uri $url -OutFile $outputPath
    Start-Sleep -Seconds 1  # Add delay to avoid rate limiting
}

Write-Host "All images have been downloaded successfully!" 