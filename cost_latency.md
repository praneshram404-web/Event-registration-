# Cost and Latency Analysis — Event Registration Cleaner

## 1. API Call Estimate

The program makes one LLM request per registration entry.

For an input file containing N registrations, the expected number of successful extraction requests is N, assuming every request succeeds.

For the supplied 20-row sample:

- Planned extraction requests: 20
- Expected requests per registration: 1
- Automatic retries: None
- Failed requests: Reported as extraction/API errors.

The actual number of successful requests may be lower if the API returns an error.

## 2. Latency

Latency depends on several factors:

- Selected language model.
- Provider server load.
- Internet connection speed.
- Prompt length.
- Response length.

Latency should be measured during an actual successful API run rather than estimated without evidence.

The average latency per request can be calculated as:

`Average latency = Total elapsed time / Number of successful requests`

Record the following information when measuring:

| Measurement | Value |
|---|---|
| Model name | gpt-4o-mini |
| Test date | Record actual test date |
| Number of input rows | 20 |
| Successful API requests | Record actual result |
| Total elapsed time | Record actual time |
| Average latency per request | Calculate from actual measurements |

If a live API run is unsuccessful, report that latency and successful-request measurements are unavailable.

## 3. Cost Estimation

The API cost depends on the selected model's current input and output token prices.

The estimated cost is calculated using:

`Estimated cost = (Input tokens / 1,000,000 × Input price per million) + (Output tokens / 1,000,000 × Output price per million)`

Before reporting a cost:

1. Check the provider's current pricing page.
2. Record the model name and pricing date.
3. Record actual input and output token usage if available.
4. Calculate the estimated cost using the applicable prices.

Do not report an assumed price as an actual project cost.

## 4. Non-LLM Processing Cost

The following operations are performed locally using Python:

- Fact-checking extracted information.
- Cleaning phone numbers and email addresses.
- Validating year and branch.
- Detecting duplicate registrations.
- Generating CSV reports.
- Generating the summary report.

These operations do not require additional LLM API requests.

## 5. Actual Project Limitation

During testing, the live API returned a `429 credit_balance_exhausted` error because the API account had no remaining credits.

Therefore:

- Live extraction could not be completed successfully.
- Actual live API latency was not measured.
- Actual live API token usage was unavailable.
- Actual live API cost could not be calculated.

The project was demonstrated using offline demonstration mode, which uses a deterministic regular-expression extractor rather than an LLM.

The offline demonstration is useful for showing the Python cleaning and reporting pipeline, but its results must not be presented as live LLM results.

## 6. Conclusion

The project separates LLM-based extraction from deterministic Python validation and reporting.

This design keeps API usage limited to information extraction while allowing cleaning, duplicate detection, and report generation to run locally.

Actual cost and latency should be measured when a successful live API run is available.