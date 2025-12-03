import math
from collections import deque
from itertools import product

class Node:
    def __init__(self, name, states):
        self.name = name
        self.states = list(states)
        self.parents = []
        self.children = []

class PestCPT:
    """Simple parametric CPT for PestOutbreak (Low, Medium, High)."""
    def __init__(self):
        self.states = ["Low", "Medium", "High"]
        # simple bias scores
        self.bias = {"Low": 1.0, "Medium": 0.0, "High": -1.0}
        # per-parent, per-state score triples (Low,Medium,High)
        self.weights = {
            "Humidity": {
                "Low": (1.0, 0.0, -1.0),
                "Medium": (0.5, 0.5, -0.5),
                "High": (-1.0, 0.0, 1.0)
            },
            "NDVI": {
                "Poor": (-0.5, 0.0, 0.5),
                "Moderate": (0.0, 0.5, -0.5),
                "Good": (1.0, 0.0, -1.0)
            },
            "PheromoneCount": {
                "Low": (1.0, 0.0, -1.0),
                "Medium": (0.0, 0.5, -0.5),
                "High": (-1.0, 0.0, 1.0)
            },
            "CropMaturity": {
                "Early": (1.0, 0.0, -1.0),
                "Mid": (0.0, 0.5, -0.5),
                "Late": (-1.0, 0.0, 1.0)
            },
            "FertilizerType": {
                "None": (-0.5, 0.0, 0.5),
                "Organic": (0.0, 0.5, -0.5),
                "Synthetic": (1.0, 0.0, -1.0)
            },
            "PesticideUsage": {
                "Low": (-0.5, 0.0, 0.5),
                "Medium": (0.0, 0.5, -0.5),
                "High": (1.0, 0.0, -1.0)
            },
            "Yield": {
                "Low": (-0.5, 0.0, 0.5),
                "Medium": (0.0, 0.5, -0.5),
                "High": (1.0, 0.0, -1.0)
            },
            "CropDiseaseStatus": {
                "None": (1.0, 0.0, -1.0),
                "Minor": (0.0, 0.5, -0.5),
                "Severe": (-1.0, 0.0, 1.0)
            }
        }

    def probs(self, parents):
        # parents: dict name->state
        scores = {}
        for s in self.states:
            val = self.bias.get(s, 0.0)
            for name, st in parents.items():
                table = self.weights.get(name)
                if not table:
                    continue
                triple = table.get(st)
                if not triple:
                    continue
                val += triple[self.states.index(s)]
            scores[s] = val
        # softmax
        m = max(scores.values())
        exps = {k: math.exp(v - m) for k, v in scores.items()}
        total = sum(exps.values())
        return {k: exps[k] / total for k in exps}

class SimpleBN:
    def __init__(self):
        self.nodes = {}
        # add nodes
        self.add_node("Humidity", ["Low", "Medium", "High"])
        self.add_node("NDVI", ["Poor", "Moderate", "Good"])
        self.add_node("PheromoneCount", ["Low", "Medium", "High"])
        self.add_node("CropMaturity", ["Early", "Mid", "Late"])
        self.add_node("FertilizerType", ["None", "Organic", "Synthetic"])
        self.add_node("PesticideUsage", ["Low", "Medium", "High"])
        self.add_node("Yield", ["Low", "Medium", "High"])
        self.add_node("CropDiseaseStatus", ["None", "Minor", "Severe"])
        self.add_node("PestOutbreak", ["Low", "Medium", "High"])
        for p in ["Humidity", "NDVI", "PheromoneCount", "CropMaturity", "FertilizerType", "PesticideUsage", "Yield", "CropDiseaseStatus"]:
            self.add_edge(p, "PestOutbreak")
        self.cpt = PestCPT()

    def add_node(self, name, states):
        self.nodes[name] = Node(name, states)

    def add_edge(self, parent, child):
        self.nodes[parent].children.append(child)
        self.nodes[child].parents.append(parent)

    def infer_pest_posterior(self, evidence):
        parents = self.nodes["PestOutbreak"].parents
        missing = [p for p in parents if p not in evidence]
        domains = {p: self.nodes[p].states for p in parents}
        if not missing:
            return self.cpt.probs({p: evidence[p] for p in parents})
        total = {s: 0.0 for s in self.nodes["PestOutbreak"].states}
        combos = product(*[domains[p] for p in missing])
        count = 0
        for combo in combos:
            vals = {p: (evidence[p] if p in evidence else v) for p, v in zip(missing, combo)}
            # ensure all parents present
            for p in parents:
                if p not in vals:
                    vals[p] = evidence.get(p)
            probs = self.cpt.probs(vals)
            for s in total:
                total[s] += probs[s]
            count += 1
        for s in total:
            total[s] /= count
        return total

    def classify_risk(self, posterior):
        best = max(posterior.items(), key=lambda kv: kv[1])
        return best[0], best[1]

    def is_d_separated(self, x, y, given):
        given = set(given)
        parents = {n: set(self.nodes[n].parents) for n in self.nodes}
        children = {n: set(self.nodes[n].children) for n in self.nodes}
        start = [(x, 'up'), (x, 'down')]
        seen = set()
        q = deque(start)
        while q:
            node, direction = q.popleft()
            key = (node, direction)
            if key in seen:
                continue
            seen.add(key)
            if node == y:
                return False
            if node not in given:
                if direction == 'up':
                    for p in parents[node]:
                        q.append((p, 'up'))
                    for c in children[node]:
                        q.append((c, 'down'))
                else:
                    for c in children[node]:
                        q.append((c, 'down'))
            else:
                if direction == 'up':
                    for p in parents[node]:
                        q.append((p, 'up'))
                else:
                    pass
        return True
