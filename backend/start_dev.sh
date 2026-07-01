#!/bin/bash
echo "Запуск бд"
sudo service docker start
docker container prune -f
docker run -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres

echo "Запуск бэкенда"
cd ~
cd project/redir_svc/backend
uvicorn src.main:app --port 8000 --reload &

echo "Запуск фронта"
cd ~
cd project/redir_svc/frontend
npm run dev -- --host 127.0.0.1 --port 3000