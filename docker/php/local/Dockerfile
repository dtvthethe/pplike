FROM php:8.3-fpm-alpine

RUN apk add --no-cache \
        oniguruma \
        libpq \
        unzip \
    && apk add --no-cache --virtual .build-deps \
        oniguruma-dev \
        postgresql-dev \
    && docker-php-ext-install -j"$(nproc)" \
        mbstring \
        pdo_pgsql \
    && apk del .build-deps

# lấy file `composer` từ image `composer:2` rồi copy vào image này, tại path `/usr/bin/composer`
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# UID/GID mặc định của user trên máy host để PHP ghi file bind mount đúng quyền.
# Có thể đổi khi build image bằng --build-arg nếu máy host dùng UID/GID khác.
ARG WWWUSER=1000
ARG WWWGROUP=1000

# Tạo user/group trong image với UID/GID ở trên.
# PHP-FPM sẽ chạy worker bằng user này thay vì root.
RUN addgroup -S -g "${WWWGROUP}" appgroup \
    && adduser -S -D -H -u "${WWWUSER}" -G appgroup appuser

# Cài cấu hình pool `www` để PHP-FPM dùng user/group vừa tạo.
COPY docker/php/local/docker.conf /usr/local/etc/php-fpm.d/www.conf

WORKDIR /var/www/html

COPY . .

# đây là port của PHP-FPM
EXPOSE 9000

CMD ["php-fpm"]
