# BÁO CÁO THỰC HÀNH LAB 2.1: MLOPS PIPELINE

**Họ và tên:** Đặng Hồ Hải  

---

## 1. Kết quả Bước 1: Thí nghiệm và Tối ưu Siêu tham số

Dựa trên quá trình thí nghiệm với MLflow UI, bộ siêu tham số (Hyperparameters) tốt nhất đã được lựa chọn để huấn luyện mô hình:

- **n_estimators:** `200`  
  → Tăng số lượng cây giúp mô hình ổn định hơn và giảm bias.

- **max_depth:** `10`  
  → Giới hạn độ sâu để tránh hiện tượng overfitting trên tập dữ liệu rượu vang.

- **min_samples_split:** `5`  
  → Đảm bảo các nút lá có đủ dữ liệu để mang tính tổng quát.

### Lý do lựa chọn

Bộ tham số này mang lại sự cân bằng tốt nhất giữa độ chính xác trên tập huấn luyện và khả năng tổng quát hóa trên tập kiểm thử thông qua các phiên chạy (Runs) trên MLflow.

---

## 2. So sánh hiệu suất: Bước 2 vs. Bước 3

### Bảng so sánh kết quả

| Chỉ số | Bước 2 (2998 mẫu) | Bước 3 (5996 mẫu) | Cải thiện (Δ) |
|---|---|---|---|
| Accuracy | 0.6440 | 0.6620 | +0.0180 |
| F1-Score | 0.6417 | 0.6583 | +0.0166 |

### Nhận xét

Khi tăng quy mô dữ liệu từ Phase 1 sang Phase 2, các chỉ số đều có sự tăng trưởng tích cực.

Điều này chứng minh hệ thống MLOps đã tự động cập nhật và cải thiện tri thức của mô hình một cách hiệu quả khi có dữ liệu mới được đẩy lên qua DVC.

---

## 3. Kỹ năng xử lý vấn đề thực tế

Trong quá trình triển khai hệ thống lên AWS EC2, tôi đã đối mặt và giải quyết các thách thức kỹ thuật sau:

### Lỗi SSH Handshake

- Nguyên nhân: định dạng `VM_SSH_KEY` trên GitHub thiếu các thẻ:
  - `-----BEGIN-----`
  - `-----END-----`

- Cách khắc phục:
  - Chuẩn hóa lại format khóa private.

### Lỗi `KeyError 'opsworkscm'`

- Nguyên nhân:
  - Xung đột phiên bản thư viện giữa `awscli` và `botocore`.

- Cách xử lý:
  - Cấu hình trực tiếp biến môi trường qua `systemd override`
  - Sử dụng `SCP` để truyền model nhị phân an toàn.

### Lỗi `"Model not loaded"`

- Nguyên nhân:
  - API khởi động trước khi model tải xong từ S3.

- Cách xử lý:
  - Kiểm tra sự tồn tại của file cục bộ trước khi khởi động service.

---

> Báo cáo được thực hiện bởi Đặng Hồ Hải — Ngày 07 tháng 05 năm 2026
