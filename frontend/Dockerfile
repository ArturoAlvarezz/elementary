FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
RUN printf 'server {\n\tlisten 80;\n\tserver_name localhost;\n\troot /usr/share/nginx/html;\n\tindex index.html;\n\tlocation / {\n\t\ttry_files $uri $uri/ /index.html;\n\t}\n\tlocation /api/ {\n\t\tproxy_pass http://sherlock-backend:5000/;\n\t\tproxy_http_version 1.1;\n\t}\n}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
