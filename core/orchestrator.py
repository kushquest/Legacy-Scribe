from services.modernization_service import ModernizationService

class ModernizationOrchestrator:
    def __init__(self):
        self.service = ModernizationService()

    async def run_modernization(self, code: str, model_name: str):
        async for step in self.service.analyze_legacy_code(code, model_name):
            yield step
