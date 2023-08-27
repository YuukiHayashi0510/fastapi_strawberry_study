## Get started

### 必須

```zsh
docker compose build
# or
docker compose up
```

### VSCode 用

Docker の環境だけだと VSCode の補完・ヒントが効かないため、
Venv をローカルに導入し、補完が効くようにしている

#### 仮想環境作成

```zsh
python3 -m venv venv
```

#### 有効化

```zsh
. venv/bin/activate
```

有効化後、Interpreter の設定を行う.

package のインストールは`pip install`で可
`pip install -r ./docker/requirements.txt`

## Alembic

### マイグレーションファイルの自動生成

1. env.py で`target_metadata = combine_metadata(User.metadata, Task.metadata)`のように Metadata を追記
1. 以下のコマンド実行

```zsh
docker compose exec api alembic revision --autogenerate -m "message"
```

### マイグレーション

#### upgrade

```zsh
docker-compose exec api alembic upgrade head
```

#### Downgrade

```zsh
docker-compose exec api alembic downgrade -1
```
