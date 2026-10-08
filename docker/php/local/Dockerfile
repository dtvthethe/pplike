FROM php:8.3-fpm-alpine

RUN apk add --no-cache \
        oniguruma \
        sqlite-libs \
        unzip \
    && apk add --no-cache --virtual .build-deps \
        oniguruma-dev \
        sqlite-dev \
    && docker-php-ext-install -j"$(nproc)" \
        mbstring \
        pdo_sqlite \
    && apk del .build-deps

# lấy file `composer` từ image `composer:2` rồi copy vào image này, tại path `/usr/bin/composer`
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

# đây là port của PHP-FPM
EXPOSE 9000

CMD ["php-fpm"]
