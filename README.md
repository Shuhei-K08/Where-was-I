# Where-was-I
"Where-was-I"は顧客情報や商談内容のメモなどを管理するアプリケーションです。 
 商談メモ欄に誰といつどのような商談をしたかなど細かく管理することができます。
 また、Todoリスト機能もあり商談メモをとりながらTodoリストの登録もでき、作業の抜け漏れを防止し、やるべきことを適切に管理することができます。

#URL

#使用技術
- python3
-　MySQL
-　apache2
-　Wisgi
-　flask
-　Docker/Docker-compose
-　AWS 
  -　VPC
  -　EC2
  
#機能一覧
-企業名の登録、閲覧
-担当者の登録、閲覧
-商談メモの作成、閲覧
-TodoListの追加、削除

- ユーザー登録、ログイン機能(devise)
- 投稿機能
  - 画像投稿(refile)
  - 位置情報検索機能(geocoder)
- いいね機能(Ajax)
  - ランキング機能
- コメント機能(Ajax)
- フォロー機能(Ajax)
- ページネーション機能(kaminari)
  - 無限スクロール(Ajax)
- 検
