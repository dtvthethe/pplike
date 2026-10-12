# RealWorld API endpoints

Nguồn: [RealWorld — Endpoints](https://realworld-docs.netlify.app/specifications/backend/endpoints/).

Có 19 endpoints. Đổi `☐` thành `☑` trong cột **Done** khi hoàn thành.

| Done | Code | Nhóm | Method | Endpoint | Chức năng | Auth | Spec | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ☐ | US_001 | User | POST | `/api/users/login` | Đăng nhập | Không |  |  |
| ☐ | US_002 | User | POST | `/api/users` | Đăng ký | Không |  |  |
| ☐ | US_003 | User | GET | `/api/user` | User hiện tại | Có |  |  |
| ☐ | US_004 | User | PUT | `/api/user` | Cập nhật user | Có |  |  |
| ☐ | PF_001 | Profile | GET | `/api/profiles/:username` | Xem profile | Tùy chọn |  |  |
| ☐ | PF_002 | Profile | POST | `/api/profiles/:username/follow` | Follow | Có |  |  |
| ☐ | PF_003 | Profile | DELETE | `/api/profiles/:username/follow` | Unfollow | Có |  |  |
| ☐ | AR_001 | Article | GET | `/api/articles` | Danh sách bài | Tùy chọn |  |  |
| ☐ | AR_002 | Article | GET | `/api/articles/feed` | Bài từ người follow | Có |  |  |
| ☐ | AR_003 | Article | GET | `/api/articles/:slug` | Chi tiết bài | Không |  |  |
| ☐ | AR_004 | Article | POST | `/api/articles` | Tạo bài | Có |  |  |
| ☐ | AR_005 | Article | PUT | `/api/articles/:slug` | Sửa bài | Có |  |  |
| ☐ | AR_006 | Article | DELETE | `/api/articles/:slug` | Xóa bài | Có |  |  |
| ☐ | CM_001 | Comment | POST | `/api/articles/:slug/comments` | Thêm bình luận | Có |  |  |
| ☐ | CM_002 | Comment | GET | `/api/articles/:slug/comments` | Các bình luận | Tùy chọn |  |  |
| ☐ | CM_003 | Comment | DELETE | `/api/articles/:slug/comments/:id` | Xóa bình luận | Có |  |  |
| ☐ | FV_001 | Favorite | POST | `/api/articles/:slug/favorite` | Yêu thích | Có |  |  |
| ☐ | FV_002 | Favorite | DELETE | `/api/articles/:slug/favorite` | Bỏ yêu thích | Có |  |  |
| ☐ | TG_001 | Tag | GET | `/api/tags` | Các tag | Không |  |  |

Auth dùng header:

```http
Authorization: Token <jwt>
```

`GET /api/articles` hỗ trợ `tag`, `author`, `favorited`, `limit`, `offset`. Feed hỗ trợ `limit`, `offset`. Mặc định: `limit=20`, `offset=0`.
