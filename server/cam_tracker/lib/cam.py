import numpy as np
from cam_tracker.models import FaceEncodings, Member

def convertEncodingsToDbRow(member_id, encodings):
    row_dict = {
        "member_id": member_id,
    }
    for i in range(1,129):
        row_dict[f'dimen{i}'] = encodings[i-1]
    return row_dict

def getMemberEncodingsFromDb(member_id):
    try:
        encodings_record = FaceEncodings.objects.get(member_id=member_id)
        encodings_dict = encodings_record.__dict__
        face_encodings = np.zeros(shape=(128,), dtype=np.float64)
        for key in encodings_dict:
            if key.startswith('dimen'):
                face_encodings[int(key.removeprefix('dimen')) - 1] = encodings_dict[key]
        return face_encodings
    except Exception as e:
        print(e)
        raise e
    
def getMembersEncodingsWithIdsFromDb(cam_id):
    try:
        members = Member.objects.filter(cam__id=cam_id)
        member_ids = []
        member_face_encodings = []
        for member in list(members):
            member_ids.append(str(member.id))
            member_face_encodings.append(getMemberEncodingsFromDb(member.id))
        return member_ids, member_face_encodings
    except Exception as e:
        print(e)
        raise e