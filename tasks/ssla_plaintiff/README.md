# ssla_plaintiff 
 **Contributor**: Jessica Wu, Jason Hegland
 
 **Source**: [SSLA](https://sla.law.stanford.edu/)
 
 **License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Extract the identities of the plaintiffs from excerpts of securities class action complaints.
 
 **Size (samples)**: 1038
 
## Task Description 

This task requires the LLM to extract the identities of plaintiffs from excerpts of securities class action complaints.

- It may be the case that the excerpt does not provide the identity of the plaintiff. In that case, the LLM should return "Not named".
- There may be multiple plaintiffs. In that case, the LLM should return the identities of all of them.

LLM outputs should be evaluated by comparing the extracted names to the ground truth. We recommend using `fuzz.partial_ratio` from the [fuzz](https://github.com/seatgeek/thefuzz) library, with a similarity score >= 80 constituting a correct answer (if a plaintiff is mentioned).
 
 
## Dataset construction
 
This task was constructed by hand, using the process described on the SSLA website.