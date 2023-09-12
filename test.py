input_list = ['Alya', 'Jasmine', 'Andrew']  
input_string = "Alya told Jasmine that Andrew could pay with cash.."

# result = []  # Danh sách kết quả

# start = 0  # Vị trí bắt đầu tìm kiếm trong chuỗi
# for word in input_list:
#     end = input_string.find(word, start) + len(word)  # Tìm vị trí kết thúc của từ trong chuỗi
#     if end == -1:  # Nếu không tìm thấy từ, thoát khỏi vòng lặp
#         break
#     result.extend([''.join([s for s in input_string[start:end] if s])])  # Tách và thêm từng từ vào danh sách kết quả
#     start = end  # Cập nhật vị trí bắt đầu cho lần tìm kiếm tiếp theo

# # Thêm phần còn lại của chuỗi (nếu còn)
# if start < len(input_string):
#     result.extend([''.join([s for s in input_string[start:] if s])])

# print(result)


# result = []  # Danh sách kết quả
#     start = 0  # Vị trí bắt đầu tìm kiếm trong chuỗi
#     for word in str_list:
#         print(word)
#         end = text.find(word, start) + len(word)  # Tìm vị trí kết thúc của từ trong chuỗi
#         print(end)
#         if end == -1:  # Nếu không tìm thấy từ, thoát khỏi vòng lặp
#             break
#         result.extend([''.join([s for s in text[start:end] if s])])  # Tách và thêm từng từ vào danh sách kết quả
#         start = end  # Cập nhật vị trí bắt đầu cho lần tìm kiếm tiếp theo
#     print(result)
#     # Thêm phần còn lại của chuỗi (nếu còn)
#     if start < len(text):
#         result.extend([''.join([s for s in text[start:] if s])])
#     for item in result:
#         if item in str_list:
#             pos_tokens.extend([(item, results[item])])
#         else:
#             pos_tokens.extend([(item, None)])
#     return pos_tokens