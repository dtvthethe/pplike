FROM node:22-alpine

WORKDIR /var/www/html

COPY package.json ./

RUN npm install

COPY . .

# đây là port của Vite dev server
EXPOSE 5173

# `tail -f` chờ theo dõi file `/dev/null`, nhưng file này không có nội dung mới nên lệnh cứ chạy để giữ container hoạt động
CMD ["tail", "-f", "/dev/null"] 
