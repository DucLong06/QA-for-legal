import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
from paraformer.my_attention import Attention


class Model_Paraformer(nn.Module):
    def __init__(self, base_model="keepitreal/vietnamese-sbert"):
        super(Model_Paraformer, self).__init__()
        self.sentenceTransformer = SentenceTransformer(base_model)
        self.attention = Attention(768)
        # self.dropout = nn.Dropout(0.5)
        self.classifier = nn.Linear(768, 2)

        self.criterion = nn.CrossEntropyLoss()

    def forward(self, query, article):
        query_vector = self.sentenceTransformer.encode(
            query, convert_to_tensor=True)
        query_vector = torch.unsqueeze(query_vector, 0)
        query_vector = query_vector.permute(1, 0, 2)

        query_vector = self.dropout(query_vector)

        article_vector = torch.stack([self.sentenceTransformer.encode(
            sentence, convert_to_tensor=True) for sentence in article])

        attention, _ = self.attention(query_vector, article_vector)
        output = self.classifier(attention)

        output = torch.squeeze(output, 1)
        return output

    def predict(self, query, article):
        with torch.no_grad():
            query_vector = self.sentenceTransformer.encode(
                query, convert_to_tensor=True)
            query_vector = torch.unsqueeze(query_vector, 1)

            article_vector = torch.stack([self.sentenceTransformer.encode(
                sentence, convert_to_tensor=True) for sentence in article])

            attention, _ = self.attention(
                query_vector.detach(), article_vector.detach())

            output = self.classifier(attention)

            output = torch.squeeze(output, 1)
            return torch.unsqueeze(torch.argmax(output, dim=1).cpu().detach(), 0)

    def get_score(self, query, article):
        with torch.no_grad():
            query_vector = self.sentenceTransformer.encode(
                query, convert_to_tensor=True)

            '''>>> torch.Size([768]) -> torch.Size([1, 1, 768])'''
            query_vector = torch.unsqueeze(query_vector, 0)
            query_vector = torch.unsqueeze(query_vector, 0)

            article_vector = torch.stack([self.sentenceTransformer.encode(
                sentence, convert_to_tensor=True) for sentence in article])
            article_vector = torch.unsqueeze(article_vector, 1)
            article_vector = article_vector.permute(1, 0, 2)

            attention, _ = self.attention(
                query_vector.detach(), article_vector.detach())

            output = self.classifier(attention)

            output = torch.squeeze(output, 1)
            return output.cpu().detach().numpy()[0][1]
