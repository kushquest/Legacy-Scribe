from services.modernization_service import ModernizationService

class ModernizationOrchestrator:
    def __init__(self):
        self.service = ModernizationService()

    async def run_modernization(self, code: str):
        async for step in self.service.analyze_legacy_code(code):
            yield step
