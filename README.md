
# POP To The Moon Bot

Register : https://t.me/PoPPtothemoon_bot/moon?startapp=7795589971

## Versi
   Versi saat ini `v1.2.6`

## Update `1.0.5` -> `1.2.6`
   1. Menambahkan fitur auto claim reff
   2. Menambahkan setingan `config.json`
   3. Membenahi beberapa tampilan dan urutan farming

## Setingan untuk config.json
|Fungsi|Deskripsi|Status|
|:-----:|:------:|:-----:|
|`farming`|Auto claim farming|Default True|
|`planet`|Auto Explore planet|Default True|
|`reff`|Auto claim reff|Default True|
|`achievements`|Auto claim achievement|Default True|
|`tasks`|Auto claim task|Default True|
|`delay_change_account`|Delay pergantian akun ,hitungannya detik bukan menit maupun milisecond|Default 30|
|`delay_iteration`|Delay iteration sama seperti delay pergantian akun namun bedanya dia untuk restarting|Default 600|

## Installation
   - Buka command prompt atau terminal, lalu jalankan perintah:
   1. Git clone project ini
      ```bash
      git clone https://github.com/livexords-nw/To-The-Moon-Bot.git
      ```
   2. Lalu masuk kedalam project
      ```bash
      cd To-The-Moon-Bot
      ```
   3. Jalankan command ini
      ```bash
      pip install -r requirements.txt
      ```
   4. Isi query To The Moon kalian di file ini `query.txt`
   5. Setelahnya jalankan botnya
      ```bash
      python bot.py
      ```

## Features
- Auto Farming
- Auto Explore Planet
- Auto Claim Achivement
- Auto Task 
- Auto Claim Reff
- Auto Daily Check-in
- Multi Account
- Loop based on the account with the fastest claim time 
