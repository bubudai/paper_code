import pandas as pd

# 获取临床数据的文本形式
def Get_text(df):
    # 构建列表 存放转换后的文本数据
    text_list = []
    # 遍历df
    for index, row in df.iterrows():
        #print(row)
        text = '患者'
        gender_dict = {0: '女', 1: '男'}
        # 性别
        if row['性别'] is not None:
            gender = gender_dict[row['性别']]
            text += '性别{}，'.format(gender)

            if gender == '男':
                text += Handle_conts_value(row, 'hb D0', 130, 175, '血红蛋白')
                text += Handle_conts_value(row, 'cr D0', 59, 104, '肌酐')
                
            if gender == '女':
                text += Handle_conts_value(row, 'hb D0', 120, 160, '血红蛋白')
                text += Handle_conts_value(row, 'cr D0', 44, 80, '肌酐')

        # APACHEII D0
        if row['APACHEII D0'] is not None:
            # 评分标准 0-20 低危 21及以上 高危
            apacheii = (float)(row['APACHEII D0'])
            if apacheii > 20:
                text += 'APACHEII高危，'
            elif apacheii <= 20:
                text += 'APACHEII低危，'
        
        # SOFA D0
        if row['SOFA D0'] is not None and pd.isna(row['SOFA D0']) is False:
            # 评分标准 0-10 低危 11及以上 高危
            sofa = (int)(row['SOFA D0'])
            if sofa > 10:
                text += 'SOFA高危，'

            elif apacheii <= 10:
                text += 'SOFA低危，'

        # 心率 D0
        if row['心率 D0'] is not None:
            # 评分标准 60-100
            heart = (float)(row['心率 D0'])
            if heart > 100:
                text += '心动过速，'
            elif heart <60:
                text += '心动过缓，'
            else:
                text += '心率正常，'

        # 三级高血压的判断
        # 只有高压值
        if row['收缩压 D0'] is not None and row['舒张压 D0'] is None and pd.isna(row['收缩压 D0']) is False:
            sbp = (int)(row['收缩压 D0'])
            if sbp >= 180:
                text += '三级高血压，'

            elif sbp >= 160:
                text += '二级高血压，'

            elif sbp >= 140:
                text += '一级高血压，'

            else:
                text += '血压正常，'


        # 只有低压值
        if row['收缩压 D0'] is None and row['舒张压 D0'] is not None and pd.isna(row['收缩压 D0']) is False:
            dbp = (int)(row['舒张压 D0'])
            if dbp >= 110:
                text += '三级高血压，'

            elif dbp >= 100:
                text += '二级高血压，'

            elif dbp >= 90:
                text += '一级高血压，'

            else:
                text += '血压正常，'

        # 高压值 和 低压值 都有
        if row['收缩压 D0'] is not None and row['舒张压 D0'] is not None and pd.isna(row['收缩压 D0']) is False:
            sbp = (int)(row['收缩压 D0'])
            dbp = (int)(row['舒张压 D0'])
            if sbp>=180 or dbp >= 110:
                text += '三级高血压，'

            elif sbp>=160 or dbp >= 100:
                text += '二级高血压，'

            elif sbp>=140 or dbp >= 90:
                text += '一级高血压，'

            else:
                text += '血压正常，'

        # 呼吸 D0
        if row['呼吸 D0'] is not None:
            # 评分标准 12-20
            breath = (float)(row['呼吸 D0'])
            if breath > 20:
                text += '呼吸急促，'

            elif breath <12:
                text += '呼吸过慢，'

            else:
                text += '呼吸正常，'

        # SPO2 D0
        if row['SPO2 D0'] is not None and pd.isna(row['SPO2 D0']) is False:
            # 评分标准 95
            spo2 = (int)(row['SPO2 D0'])
            if spo2 >= 95:
                text += '血氧正常，'

            else:
                text += '低血氧，'

        # 补液试验 D0
        if row['补液试验 D0'] == '1':
            text += '补液实验，'

        # 镇静治疗 D0
        if row['镇痛治疗 D0'] == '1':
            text += '镇痛治疗，'

        text += Handle_conts_value(row, 'alb D0', 35, 55, '白蛋白')
        text += Handle_conts_value(row, 'na D0', 135, 145, '钠离子')
        text += Handle_conts_value(row, 'cl D0', 95, 105, '氯离子')
        text += Handle_conts_value(row, 'lac D0', 0.5, 2.2, '乳酸酸性')
        text += Handle_conts_value(row, 'bun D0', 2.5, 7.1, '尿素氮')
        text += Handle_conts_value(row, 'po2 D0', 75, 100, '动脉氧分压')
        if not pd.isna(row['bmi']):
            text += Handle_conts_value(row, 'bmi', 18.5, 23.9, 'BMI')

        text_list.append(text+ '\t{}'.format(row['label']) + '\n')

    return text_list
        
# 统一处理连续型变量
def Handle_conts_value(row, item, min, max, des):
    if row[item] is not None:

        value = (float)(row[item])
        if value > max:
            return '{}过高，'.format(des)

        elif value < min:
            return '{}过低，'.format(des)
        
        else:
            return '{}正常，'.format(des)
    
    else:
        return ''

# 读取没有标题行的CSV文件
df_train = pd.read_csv(r'D:\项目\安医大一附院重症脓毒症\脓毒症分型与预测\基于文本分类预测\train.csv')

with open('train.txt', 'w', encoding='utf8') as f:
    for text in Get_text(df_train):
        f.write(text)

# 读取没有标题行的CSV文件
df_train = pd.read_csv(r'D:\项目\安医大一附院重症脓毒症\脓毒症分型与预测\基于文本分类预测\test.csv')

with open('test.txt', 'w', encoding='utf8') as f:
    for text in Get_text(df_train):
        f.write(text)
