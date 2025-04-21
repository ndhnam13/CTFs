# Mô tả
My Rayhunter has only been in operation for about 3 months, yet it's alerted 4 times! The EFF warns that Rayhunter packet captures "may contain sensitive information such as your IMSI and the unique IDs of cell towers you were near which could be used to ascertain your location at the time". Think you can figure out where I was when my Rayhunter alerted?

Flag format: DawgCTF{IMSI_IMEI_zipcode}

# Phân tích
IMSI ở packet số 28

IMEISV(16 số) ở packet số 36, Đề bài yêu cầu IMEI nên ta sẽ phải tìm IMEI này từ IMEISV, đưa vào web https://www.imei.info/?imei=353977577332846

Biết được đây là IMEI hợp lệ (Đoạn này có kẹt lúc đầu vì tưởng chỉ cần xoá 2 số cuối là ra IMEI nhưng thực ra IMEI có format 15 số tức là phải có thêm 1 số CD(Check digit) vào cuối sau khi đã xoá 2 số cuối từ IMEISV, may là cái web trên đã làm hộ)

Còn lại muốn tìm ra zipcode thì có thể truy qua các cellID và tracking area code, trong wireshark filter = `gms_a.imeisv` có 4 lần nhả IMEISV, như đã biết trên phần mô tả thì có nói đến việc bị alert 4 lần, quay lại các packet có xuất hiện IMEISV, lướt lên một chút tìm các packet có info `SystemiInfomationBlockType1` rồi sau đó check các mã MCC, MNC, LAC, và CELL ID, phải quy hết về decimal 

Sau đó đưa vào web https://findcellid.com/

Dưới đây đã tìm ra kết quả mà 2 điểm này có bán kính giao nhau, tìm trên https://www.unitedstateszipcodes.org/ thấy rằng 1 là nằm trong khu vực có zip code `20740` hoặc là `20742` ở đây ta chọn zipcode thứ 2

```
MCC	MNC	LAC	CELL ID	Bán kính	
310	260	20440	11531527	154.78	
311	480	27395	27419662	79.62	
```

# Flag
IMSI: 310240191383963

IMEI: 353977577332846

Zipcode: 20742

`DawgCTF{310240191383963_353977577332846_20742}`