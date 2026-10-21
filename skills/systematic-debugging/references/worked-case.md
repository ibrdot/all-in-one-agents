# Worked case: retries duplicate an order

## Symptom and baseline
A payment callback times out. A retry creates a second order. Reproduce with a
fake payment provider that records success and then raises a transport timeout.
The regression must assert one business order after two identical callbacks,
not merely that both HTTP responses are successful.

## Competing hypotheses
1. The retry changes the business key: log the stable callback identifier.
2. The handler checks for existence outside its transaction: force concurrent
   callbacks with a barrier immediately after the lookup.
3. The provider committed despite its timeout: separate transport outcome from
   business outcome in the fixture.

Change one variable per experiment. A delay that makes the race disappear is
not a fix. Do not add a blanket retry around the whole transaction.

## Repair and evidence
Use a database uniqueness constraint on the business idempotency key, then
handle an existing order by returning its original result. A process-local lock
cannot protect multiple workers. Test sequential duplicates, concurrent
duplicates, a genuine provider rejection, and recovery after worker restart.
Keep the initial failure output, exact reproducer, fix revision, and final suite
output. If the hypothesis was wrong, discard the patch rather than defending it.
