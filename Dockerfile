# Use a lightweight Nginx Alpine image to serve static files
FROM nginx:alpine

# Remove default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy all static site files directly to Nginx's serving directory
# This is a pure static site (HTML/CSS/JS) - no build step needed
COPY . /usr/share/nginx/html/

# Nginx config to handle HTML routes without .html extension
RUN printf 'server {\n\
    listen 80;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    \n\
    # Serve .html files without extension in URL\n\
    location / {\n\
        try_files $uri $uri/ $uri.html =404;\n\
    }\n\
    \n\
    # Serve project-modals directory\n\
    location /project-modals/ {\n\
        alias /usr/share/nginx/html/project-modals/;\n\
    }\n\
    \n\
    # Cache static assets\n\
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|webp|svg|woff|woff2|mp4|mov)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, immutable";\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
