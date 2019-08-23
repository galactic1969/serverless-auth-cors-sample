# これは何

Serverless FrameworkでCORSに対応しつつ、Custom Authorizerを利用するときのサンプルです。

# 環境構築

## 1. Configの記入

```yml
aws:
  account: AWSアカウント番号
  region: ap-northeast-1
kms:
  arn: arn:aws:kms:ap-northeast-1:xxx:key/xxx  # 初回デプロイ後に記入
api:
  auth_key: xxx  # Headerの認証キー
  allow_ip_address: 0.0.0.0, 1.1.1.1  # APIで許可するIPアドレス。複数書く場合はカンマ区切り
```

## 2. Deploy

```sh
$(npm bin)/sls deploy
```

※本番環境の場合は `--stage prod` をつける

## 3. KMS のARNを確認する

デプロイ後、KMSのキーが出来上がっているので確認して、ARNをconfigに反映します。

## 4. 再度Deploy

```sh
$(npm bin)/sls deploy
```

## 5. テスト

test/req.http を参照してください。
VSCodeのExtension [RestClient](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) を使うとそのままリクエストを送信できます。
