import os
import easyocr
import warnings
import pixellib
from pixellib.torchbackend.instance import instanceSegmentation

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
warnings.filterwarnings("ignore")


# -----------------------------

def text_recognition(file_path, text_file_name="result.txt"):
    reader = easyocr.Reader(["ru", "en"])
    result = reader.readtext(file_path, detail=0, paragraph=True)

    # with open(text_file_name, "w") as file:
    #     for line in result:
    #         file.write(f"{line}\n\n")

    return result


def prediction_processing(ans, sort = True):
    main_obj = ans[0]['class_names'][0]
    ans_1 = (ans[0]['class_names'], ans[0]['scores'])
    if sort:
        ans_1 = [
                    (
                        ans_1[0][i],
                        ans_1[1][i].item(),
                        (ans[0]['boxes'][i][2] - ans[0]['boxes'][i][0]) * (ans[0]['boxes'][i][3] - ans[0]['boxes'][i][1])
                    ) for i in range(len(ans_1[0]))
                ][:10]
        ans_1.sort(key=lambda x: -x[2])

    # сортировка по площади (можно ускорить: убрать сорт)
    return ans_1[0][0]




def basic_mode(model_path="/Users/semyonemakov/PycharmProjects/misha_ml/rcnn/pointrend_resnet50.pkl",
               img_path="/Users/semyonemakov/PycharmProjects/misha_ml/rcnn/38-e1442841344600.jpg"):
    # ins = instanceSegmentation()
    # ins.load_model(model_path)

    # t_g = ins.select_target_classes(car=True)
    ans = ins.segmentImage(img_path)
    #   print(ans)
    return prediction_processing(ans, True)


def text_mode(img_path="38-e1442841344600.jpg", text_file_name="result.txt"):
    return text_recognition(file_path=img_path)


def run(mode='basic', img_path="/Users/semyonemakov/PycharmProjects/misha_ml/rcnn/38-e1442841344600.jpg",
        text_file_name="result.txt"):
    ANS = ''
    if mode == 'basic':
        ANS = basic_mode(img_path=img_path)
    elif mode == 'text':
        ANS = text_mode(img_path=img_path, text_file_name="result.txt")

    print(ANS)


# ------------------------------------------------------------------------------------------

# img_path = "/Users/semyonemakov/PycharmProjects/misha_ml/rcnn/38-e1442841344600.jpg"

# mode = input()
# run(mode)
model_path="/Users/semyonemakov/PycharmProjects/misha_ml/rcnn/pointrend_resnet50.pkl"
ins = instanceSegmentation()
ins.load_model(model_path)
for i in range(100):
    run()
