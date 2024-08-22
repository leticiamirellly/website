import ray
from ray.runtime_env import RuntimeEnv
from ray.util import ActorPool
from langchain_community.embeddings import HuggingFaceEmbeddings
import asyncio

runtime_env = RuntimeEnv(
    pip=["emoji"],
    env_vars={"TF_WARNINGS": "none"})

RuntimeEnv(conda={
    "channels": ["defaults"],
    "run_options": ["--cap-drop SYS_ADMIN","--log-level=debug"]})

ray.init(ignore_reinit_error=True, log_to_driver=False)

@ray.remote
class EmbedChunks:
    def __init__(self):
        self.print_cluster_resources()
        
        self.embed_model = HuggingFaceEmbeddings(
            model_name="thenlper/gte-base",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"device": "cuda", "batch_size": 100}
        )
        ray.init(ignore_reinit_error=True, log_to_driver=False)
        
    def print_cluster_resources(self):
        cluster_resources = ray.cluster_resources()
        available_resources = ray.available_resources()

        print("Total Cluster Resources:", cluster_resources)
        print("Available Resources:", available_resources) 
          
    async def run_concurrent(self):
        print("started")
        await asyncio.sleep(0.1) # concurrent workload here
        print("finished")   
       
 
    async def process(self, batch):
        print('BATCH',batch)
        # return batch
        # embeddings = self.embed_model.embed_documents(batch["text"])
        # return embeddings
        # return {"text": batch["text"], "embeddings": embeddings}
