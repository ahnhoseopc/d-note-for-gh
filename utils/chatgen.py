import requests
import utils.config as config

CHATURL = None
def init_chatgen():
    global CHATURL
    CHATURL = config.get_option("apis.chat_api")

init_chatgen()

def generate(query):
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url=CHATURL, headers=headers,json={"query": query} )
        response.raise_for_status()

        # 응답 데이터 출력
        print("응답 코드:", response.status_code)
        print("응답 본문:", response.json())
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        print("응답 코드:", response.status_code)
        print("응답 본문:", response.text)

    except requests.exceptions.ConnectionError:
        print("연결 오류 발생. 서버에 접근할 수 없습니다.")

    except requests.exceptions.Timeout:
        print("요청 시간이 초과되었습니다.")

    except requests.exceptions.RequestException as err:
        print(f"알 수 없는 오류 발생: {err}")

    return None

if __name__ == "__main__":
    prompt = """
    입력된 데이터의 "present illness" 와 "plan"을 확인하여 "operation name"을 추정하라.
    추정된 "operation name"을 참조하여 "operation protocols"의 "code" 또는 "code name"과 대응하는 것을 찾아서 해당하는 "protocol"을 찾아라.
    응답으로 "present illness" 와 "plan", "operation name"과 "code", "code name", "protocol"을 제시하라.
    """

    data = """{
        "patient": {
            "patient id": "1135806 ",
            "date of admission": "20250123",
            "sex": "M",
            "age": "64"
        },
        "clinical staff": {
            "department": "NS",
            "doctor in charge": "002702",
            "physician assistant": null,
            "nurse": null,
            "anesthesiologist": null,
            "method of anesthesia": null
        },
        "subjective": {
            "chief complaints": "LBP with rt. buttock/thigh/leg pain",
            "pain": "1$6^0$^0$^0^1^",
            "onset": "for 4-5 months",
            "present illness": "\uc77c\uc0c1\uc0dd\ud65c \ubd88\uac00\ub2a5\ud560 \uc815\ub3c4\ub85c LBP with rt. buttock/thigh/leg pain \uc2ec\ud558\uc5ec \uc218\uc220\uc704\ud574 \uc785\uc6d0\ud568",
            "obsteric gpal": null,
            "menstrual history": null,
            "past medical history": "^0",
            "admission-operation history": null,
            "social history": null,
            "family history": "1$0$^"
        },
        "objective": {
            "review of systems": null,
            "other review of systems": null
        },
        "assessment": {
            "impression": "1. \uc2e0\uacbd\ubfcc\ub9ac\ubcd1\uc99d\uc744 \ub3d9\ubc18\ud55c \uc694\ucd94 \ubc0f \uae30\ud0c0 \ucd94\uac04\ud310\uc7a5\uc560<G55.1*>",
            "diagnosis": [
                null
            ]
        },
        "plan": {
            "operation name": null,
            "plan": "L4-5, rt, discectomy",
            "discharge plan": null,
            "educational plan": "\uc9c8\ud658\uc0c1\ud0dc, \uce58\ub8cc\uacc4\ud68d, \uce58\ub8cc\uc5d0 \ub530\ub978 \uc608\uc0c1\ud6a8\uacfc \ubc0f \uc704\ud5d8\uc5d0 \ub300\ud574 \uad50\uc721\ud568."
        },
        "report date": "20250123",
        "report time": "11:41:49",

        "operation protocols": [
            {
                "code": "A01                 ",
                "code_name": "Lumbar",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Small laminotomy with discectomy ( L )\r\n5. Decompressive laminotomy ( L )\r\n(Unilateral laminotomy for bilateral decompression)\r\n5. Decompressive foraminotomy ( L )\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A02                 ",
                "code_name": "PLIF",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. L PLIF \r\n1) Lt. laminotomy for bilateral decompression \r\n: adhesion & inflmmmation, severe\r\n2) facetectomy/ discectomy\r\n3) Cage interbody insertion \r\n: transversely lying \r\n: autologous bone + allograft + DBM\r\n6. Percutaneous screw fixation (6.5mm X 45mm)\r\n7. Bleeding control, irrigation\r\n8. Hemovac 100cc\r\n9. Suture\r\n}\r\n"
            },
            {
                "code": "A11                 ",
                "code_name": "Cervical",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position with slightly flexed neck\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Small laminotomy\r\n5. Discectomy ( C )\r\n1) ruptured disc (+)\r\n2) adhesion, severe\r\n5. Decompressive foraminotomy ( C )\r\n5. Decompressive laminotomy ( C )\r\n(unilateral laminotomy with bilateral decompression)\r\n5. Decompressive hemilaminectomy with contralateal sublaminoplasty \r\nwith total flacectomy ( C )\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A21                 ",
                "code_name": "Thoracic",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position \r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Decompressive laminotomy\r\n5. Removal of OLF ( T ) through translaminar approach\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A31                 ",
                "code_name": "VP",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Clean drapping\r\n4. Small skin incision\r\n5. L2 VP\r\n6. Suture\r\n}\r\n"
            },
            {
                "code": "A32                 ",
                "code_name": "Irrigation",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Clean drapping\r\n4. I & D\r\n5. Hemovac 100cc\r\n6. Suture\r\n}\r\n"
            },
            {
                "code": "A41                 ",
                "code_name": "NAVI",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Catheter insertion into epidural space though trans-sacral hiatus (with NAVI)\r\n4. Position of catheter checked with C-ram radiography and dye\r\n5. Epidural neuroplasty was performed under the C-arm\r\n6. Several drugs apply\r\n7. Suture and dressing\r\n}\r\n"
            }
        ]
    }
    """

    prompt = "최근 고시를 알려줘"
    data = "2024년도 고시"
    response = generate([prompt, data])
    print(dir(response))
    print(response, end="\t")
