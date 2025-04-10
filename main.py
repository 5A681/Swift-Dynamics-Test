
# เลขในภาษาไทย
thai_number = ("ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า")
# หน่วยในภาษาไทย
thai_unit = ("", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน")
class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if number < 0:
            return 'output = number can not be negative'
        fac = self.__factorial(number)   
        # เมื่อ ค่า factorial นำไปนับเลข 0 ที่อยู่ท้าย   
        count = self.__count_zero(str(fac))
        return count
    
    def find_max_index(self, numbers: list) -> int | str:
        
        if len(numbers) == 0:
           return 'list can not blank'
        return self.__find_max_value_index(numbers=numbers)
    def __find_max_value_index(self,numbers: list) -> int:
       indexMax = 0
       maxValue = 0
       for i in range(len(numbers)):
          # ถ้าค่าปัจจุบันมากกว่าค่าที่เก็บไว้ ให้นำค่าปัจจุปับนไปเป็นค่ามากสุด และให้ indexMax คือ index ที่มีค่ามากที่สุด
          if numbers[i] > maxValue:
             indexMax = i
             maxValue = numbers[i]
       return indexMax
    
    # ฟังก์ชั่น สำหรับหา factorial
    def __factorial(self,number :int) -> int:
        if number == 0:
            return 1
        # ใช้ recursive function หาค่า factorial
        fac = number *  self.__factorial(number=number-1)
        return fac

    def __count_zero(self,num :str) -> int:
         
         count = 0
         # นับค่า 0 จากข้างหลังแล้วเพิ่มค่าเรื่อยๆ เมื่อไม่ใช่ 0 แล้วให้หยุด
         for i in range(len(num) - 1, -1, -1):
          if num[i] == '0':
            count += 1
          else:
            break
         return count
    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return 'number can not less than 0'
        s_number = str(number)[::-1]

        #สร้าง ชุดข้อมูล สำหรับแปลงเป็นภาษาไทย โดยแปล่งของเป็นชุดละ 6 ตัว ถ้าเลขข้างหน้ามีแค่ 0 จะไม่เอามา
        n_list = [s_number[i:i + 6].rstrip("0") for i in range(0, len(s_number), 6)]

        # นำชุดข้อมูลชุดที่ 1 ที่ไม่ใช่หลักล้านเข้าฟังก์ชั่นสำหรับแปลงตัวเลข
        result = self.__unit_process(n_list.pop(0))
        for i in n_list:
            #หลังจากข้อมูลชุดแรก ชุดต่อไปจะเป็นหลักล้าน ดังนั้น ผลลับจะต้องมี ล้าร ตามหลังเสมอ
            result = self.__unit_process(i) + 'ล้าน' + result

        return result
    def __unit_process(self,value):
        length = len(value) > 1
        result = ''
        # index คือ ตำแหน่ง ของตัวเลข  current คือตัวเลขนั้นๆ
        for index, current in enumerate(map(int, value)):
            # ถ้าตัวเลขไม่ใช่ 0
            if current:
                # ถ้า index ไม่ใช่ 0
                if index:
                    #จะใส่หน่วยก่อน เช่น 50 index คือ 1 อยู่ตำแหน่งที่ 1 คือ สิบ แล้ว หน้าจะใส่หลังจากนี้ อยู่ส่วนของ elif ข้างล่าง
                    result = thai_unit[index] + result
                # ถ้าตัวเลขในชุดข้อมูลมีมากกว่า 1 ตัว และ 1 คือตัวที่อยู่หลังสุด
                if length and current == 1 and index == 0:
                    result += 'เอ็ด'
                # ถ้า 2 คือ ตัวที่อยู่ลำดับที่ 2
                elif index == 1 and current == 2:
                    result = 'ยี่' + result
                
                # หลังจากนั้น ถ้า index และ ค่า current ไมใช่ 1 ให้ใส่ตัวเลขแปลงเป็นไทย
                elif index != 1 or current != 1:
                    result = thai_number[current] + result
                
        return result
    def number_to_roman(self, number: int) -> str:
        if number <0:
            return 'number can not less than 0'
        val = [
        1000, 900, 500, 400,
        100,  90,  50,  40,
        10,   9,   5,   4, 1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV", "I"
        ]
        roman_num = ""
        i = 0
        while number > 0:
            # count คือจำนวนของจัวเลชโรมันซ้ำ
            count = number // val[i]
            #เลขโรมันจะซ้ำเท่ากับจำนวน count
            roman_num += syms[i] * count

            #เอาตัวเลขที่เหลืออยู่ ลบด้วยค่าที่หาเสร็จแล้วออก เช่น 320 ถ้าเราหา 20 = XX เสร็จแล้วให้ลบออก 20 แล้วหา 300 ต่อ
            number -= val[i] * count
            i += 1
        return roman_num

    






solution = Solution()

# ข้อ 1
print("tailing_zeroes is ",solution.find_tailing_zeroes(number=10))

# ข้อ 2
input = [1,2,1,3,5,6,4]
print("index for max value is ",solution.find_max_index(input))

# ข้อ 3
print(solution.number_to_thai(-1))

# ข้อ 4
print(solution.number_to_roman(35))