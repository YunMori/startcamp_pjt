# 빌드 컨텍스트: 저장소 루트 (docker-compose.yml 참고)
FROM node:22-alpine AS build
WORKDIR /app
COPY front/package.json front/package-lock.json ./
RUN npm ci
COPY front/ ./

# VITE_ 값은 빌드 타임에 번들에 박힘. 빈 문자열은 http.js의 || 폴백에 걸리므로 '/' 사용
ARG VITE_API_BASE_URL=/
ARG VITE_KAKAO_JS_KEY
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_KAKAO_JS_KEY=$VITE_KAKAO_JS_KEY
RUN npm run build

FROM nginx:1.27-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
