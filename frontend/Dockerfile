FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
RUN echo 'server {\n\tlisten 80;\n\tserver_name localhost;\n\troot /usr/share/nginx/html;\n\tindex index.html;\n\tlocation / { try_files $uri $uri/ /index.html; }\n\tlocation /api/ { proxy_pass http://sherlock-backend:5000/; proxy_http_version 1.1; }\n}' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
