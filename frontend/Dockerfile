# BUILDER
FROM node:18-alpine as builder-base
WORKDIR /frontend
COPY ./package.json package-lock.json ./
RUN npm install
COPY . ./
ARG REACT_APP_API_URL

# Create env file
RUN \
    if ([ -z "$REACT_APP_API_URL" ]); \
    then echo 'Set environment variables for frontend' &&  exit 1; \
    else \
        echo REACT_APP_API_URL=$REACT_APP_API_URL >> ./.env && \
        echo TZ=Europe/Moscow >> ./.env; \
    fi

RUN npm run build

# NGINX
FROM nginx:1.23-alpine as production

COPY --from=builder-base /frontend/build/ /usr/share/nginx/html
COPY --from=builder-base /frontend/nginx.conf /etc/nginx/conf.d/default.conf
