class DecisionEngine:

    def bepaal_actie(self, context):

        # Geen beweging?
        if not context.bewegend():
            return "GEEN_ACTIE"

        # Overdag geen interventie
        if not context.nacht:
            return "GEEN_ACTIE"

        # 's Nachts en persoon beweegt
        return "OPVOLGEN"
