# Description: Download Twitter profile
# Usage: ./download_twitter_profile.sh

# Change the environment settings in the .env file, or set it manually
# via ENVIRONMENT env variable as "production" before running the script

# Download LinkedIn profile
ice-breaker download-profile linkedin https://www.linkedin.com/in/yann-lecun/  --force-scraping
