FROM nginx:latest

ENV GREETING="Default Welcome Message"
# Overwrite the default Nginx HTML with our variable, then start Nginx
CMD echo "$GREETING" > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'