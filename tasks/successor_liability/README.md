# successor_liability

### Given a fact pattern, identify the type of successor liability present.
---


**Source**: Frank Fagan

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 50

**Legal reasoning type**: Application/conclusion

**Task type**: 4-way classification

## Task description

When one company sells its assets to another company, the purchaser is generally not liable for the seller’s debts and liabilities. Successor liability is a common law exception to this general rule. In order to spot a successor liability issue, lawyers must understand how courts apply the doctrine.

The doctrine holds purchasers of all, or substantially all, of a seller’s assets liable for the debts and liabilities of the seller if:

1. the purchaser expressly agrees to be held liable;

2. the assets are fraudulently conveyed to the purchaser in order to avoid liability;

3. there is a de facto merger between the purchaser and seller; or

4. the purchaser is a mere continuation of the seller.

Express agreement is governed by standard contract law rules. In practice, if a purchase agreement contains a provision to assume liabilities, litigation will rarely arise. Courts, however, sometimes interpret express agreement in the absence of a written provision. 

Assets are fraudulently conveyed when the seller intends to escape liability through an asset sale or knows that liability will be avoided through an asset sale.

De facto merger is a multifactor test that consists of (1) continuity of ownership; (2) cessation of ordinary business and dissolution of the acquired corporation as soon as possible; (3) assumption by the purchaser of the liabilities ordinarily necessary for the uninterrupted continuation of the business of the acquired corporation; and (4) continuity of management, personnel, physical location, assets, and general business operation. Some jurisdictions require a showing of all four elements. Others do not and simply emphasize that the substance of the asset sale is one of a merger, regardless of its form.

Mere continuation requires a showing that after the asset sale, only one corporation remains and there is an overlap of stock, stockholders, and directors between the two corporations. There are two variations of the mere continuation exception. The first is the “continuity of enterprise” exception. In order to find continuity of enterprise, and thus liability for the purchaser of assets, courts engage in a multifactor analysis. Factors include: (1) retention of the same employees; (2) retention of the same supervisory personnel; (3) retention of the same production facilities in the same physical location; (4) production of the same product; (5) retention of the same name; (6) continuity of assets; (7) continuity of general business operations; and (8) whether the successor holds itself out as the continuation of the previous enterprise. The second is the product line exception. This exception imposes liability on asset purchasers who continue manufacturing products of a seller’s product line. This exception generally requires that defendants show that the purchaser of assets is able to assume the risk-spreading role of the original manufacturer, and that imposing liability is fair because the purchaser enjoys the continued goodwill of the original manufacturer. 

## Dataset construction

A dataset was constructed in order to test a model's ability to spot a successor liability issue. The dataset was constructed by hand, inspired by standard law school examination questions that require students to identify successor liability as a potential legal issue arising in an asset purchase.

The dataset consists of four types of fact patterns. Each represent the standard exceptions to the general rule that purchasers of assets are not responsible for the debts and liabilities of the seller. These include: express agreement, fraudulent conveyance, de facto merger, and mere continuation.

## Data column names

- `answer`: successor liability issue
- `issue`: whether the fact pattern pertains to successor liability
- `text`: fact pattern