from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity


class ImageHandler:
    def __init__(self):
        self.mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def checking_face_on_image(self, img, mess='None'):
        face, prob = self.mtcnn(img, return_prob=True)
        if face is not None and prob > 0.90:
            emb = self.resnet(face.unsqueeze(0))
            return emb
        else:
            print(f"Лицо на картинке {mess} не обнаружено")
            return None

    def authentication(self, image_true, image_now):
        image_true_embed = self.checking_face_on_image(image_true, mess='true_img')
        if image_true_embed is None:
            return None
        image_now_embed = self.checking_face_on_image(image_now, mess='now_img')
        if image_now_embed is None:
            return None

        dist = cosine_similarity(image_true_embed.detach(), image_now_embed.detach())
        if dist > 0.7:
            return True
        return False