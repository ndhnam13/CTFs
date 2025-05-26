# Mô tả

We're currently in the midst of a murder investigation, and we've obtained the victim's phone as a key piece of evidence. After conducting interviews with witnesses and those in the victim's inner circle, your objective is to meticulously analyze the information we've gathered and diligently trace the evidence to piece together the sequence of events leading up to the incident.

# Phân tích

Bài này có thẻ làm theo 2 cách, 1 là check các file có liên quan tới nội dung app của câu hỏi kết hợp với `DB browser` để xem database hoặc dùng [ALEAPP](https://github.com/abrignoni/ALEAPP/releases/tag/v3.4.0) để nó tự quét và tạo report cho mình, tôi dùng ALEAPP cho tiện. Thực ra cái cách thứ 2 chỉ là tool tự động hoá của cái thứ nhất thôi nhưng do bài này phân tích file máy android nên có sẵn tool rồi

## Flag 1

Based on the accounts of the witnesses and individuals close to the victim, it has become clear that the victim was interested in trading. This has led him to invest all of his money and acquire debt. Can you identify the `SHA256` of the trading application the victim primarily used on his phone?

Trong phần `Installed Apps for user 0` hoặc là `\data\app\com.ticno.olymptrade-lKDfBXc8qLNF9F2eXSyBwg==` rồi sau đó `sha256sum base.apk` 

Người dùng sử dụng app `olymptrade` để mua bán crypto

4f168a772350f283a1c49e78c1548d7c2c6c05106d8b9feb825fdc3466e9df3c

## Flag 2

According to the testimony of the victim's best friend, he said, "`While we were together, my friend got several calls he avoided. He said he owed the caller a lot of money but couldn't repay now`". How much does the victim owe this person?

Kiểm tra data của `olymptrade` thì không thấy có database tin nhắn nên tôi chuyển sang tìm cái khác, có discord nhưng như vậy lỡ tìm luôn cho mấy flag sau rồi, đáp án của câu hỏi này nằm ở `\data\user_de\0\com.android.providers.telephony\databases\mmssms.db` trong các tin nhắn SMS có 1 tin nhắn

```
It's time for you to pay back the money you owe me, but you're not picking up my calls. You better think twice about not paying, because it won't end well for you. Prepare the sum of 250,000 EGP, and I'll expect your call within an hour at most.	
```

`250000`

## Flag 3

What is the name of the person to whom the victim owes money?

Trong phần `Contacts` và `Call logs` hoặc là `\data\data\com.android.providers.contacts\databases\contacts2.db` và `\data\data\com.android.providers.contacts\databases\calllog.db`

Ở trên có nói rằng người dùng nhận được nhiều cuộc gọi nhưng không trả lời với từ chối thì ta có thể thấy khoảng `2023-09-20 19:35` thì có rất nhiều cuộc gọi bị missed với rejected từ số `+201172137258` đối chiều lại trong contact ta có kết quả

`Shady Wahab`

## Flag 4

Based on the statement from the victim's family, they said that on `September 20, 2023`, he departed from his residence without informing anyone of his destination. Where was the victim located at that moment?

Trong `Recent activity 0` hoặc `\data\system_ce\0\recent_tasks` ảnh `6.jpg` có hiện vị trí hiện tại của người dùng vào `2023-09-20 23:50:29`

`The Nile Ritz-Carlton`

## Flag 5

The detective continued his investigation by questioning the hotel lobby. She informed him that the victim had reserved the room for 10 days and had a flight scheduled thereafter. The investigator believes that the victim may have stored his ticket information on his phone. Look for where the victim intended to travel.

Trong `C:\Users\admin\Desktop\temp_extract_dir\data\media\0\Download\Plane Ticket.png` có địa chỉ mà người dùng muốn bay đến

`Las Vegas`

## Flag 6

After examining the victim's Discord conversations, we discovered he had arranged to meet a friend at a specific location. Can you determine where this meeting was supposed to occur?

Trong `Discord Chats` hoặc `\data\data\com.discord\files\kv-storage\@account.665825323065016370\a` có tin nhắn từ người dùng `rob1ns0n` về việc chuyển địa điểm gặp mặt

```
What a wonderful news! We'll meet at **The Mob Museum**, I'll await your call when you arrive. Enjoy you flight bro ❤️
```

`The Mob Museum`