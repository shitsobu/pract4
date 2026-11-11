# Attendance — практическая работа № 4, вариант 6

Приложение для учета посещаемости. Читает CSV с колонками `name,start,end` и рассчитывает длительность присутствия в минутах, включая переход через полночь.

## Запуск
```bash
python attendance.py --help
python attendance.py --duration 22:30 01:15
python attendance.py attendance.csv.example
```
Ожидаемый результат команды `--duration 22:30 01:15`: `165`.

## Тестирование
```bash
python -m unittest discover -s tests -v
```
В проекте 11 модульных тестов, в том числе `test_duration_crosses_midnight`.

## Docker
```bash
docker build -t attendance-app .
docker run --rm attendance-app --help
```

## GitHub Actions
Workflow: `.github/workflows/ci.yml`.

- `validate`: Pull Request в `main` и push в `main`; компиляция Python и проверка UTF-8.
- `unit_tests`: Pull Request, push в `main` и Scheduled workflow.
- `package`: push в `main`, push тега и Scheduled workflow; артефакт хранится 7 дней.
- `deploy_test`: ручной запуск через Actions → Attendance CI/CD → Run workflow; разрешена только ветка `main`.

### Секреты и переменные
В Settings → Secrets and variables → Actions создай Secret `DEPLOY_TOKEN` (тестовое значение). Секрет не выводится в журнал. `APP_PORT=8106` задан в workflow.

### Расписание
Cron `0 6 * * 1` запускает workflow каждый понедельник в 06:00 UTC. По расписанию выполняются `unit_tests` и `package`.

### Ручное развертывание
Открой Actions → Attendance CI/CD → Run workflow, выбери `main`. Задание deploy_test скачает артефакт, проверит секрет, скопирует файлы в `deploy/test` и выполнит smoke test.
