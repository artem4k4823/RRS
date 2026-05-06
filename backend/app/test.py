import asyncio
import asyncpg

async def main():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="ваш_реальный_пароль",  # замените
            database="melwiki",
            host="localhost",
            port=5435
        )
        print("✅ Успешно подключились!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

asyncio.run(main())