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

#Later kunnen we die uitbreiden naar bijvoorbeeld:
#GEEN_ACTIE
#    │
#    ├── overdag
#    │
#    └── geen beweging

#OPVOLGEN
#    │
#    └── nacht + beweging

#AANDACHT
#    │
#    └── meerdere zones kort na elkaar

#INTERVENTIE
#    │
#    └── richting uitgang + nacht
