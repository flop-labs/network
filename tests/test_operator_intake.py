"""Protect public intake routing and evidence boundaries."""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueLoader(yaml.BaseLoader):
    """Also reject duplicate mapping keys that YAML normally silently overwrites."""

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f"duplicate YAML key: {key}")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def load(path):
    return yaml.load((ROOT / path).read_text(), Loader=UniqueLoader)


class OperatorIntakeTests(unittest.TestCase):
    def setUp(self):
        self.form = load(".github/ISSUE_TEMPLATE/operator-application.yml")
        self.fields = {
            field["id"]: field for field in self.form["body"] if "id" in field
        }
        self.labels = {label["name"]: label for label in load(".github/labels.yml")}

    def test_every_form_applies_only_defined_labels_and_has_unique_fields(self):
        definitions = load(".github/labels.yml")
        self.assertEqual(len(definitions), len(self.labels))
        for label in definitions:
            self.assertRegex(label["color"], r"^[0-9a-fA-F]{6}$")
            self.assertTrue(label["description"])
        for path in (ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"):
            form = load(path.relative_to(ROOT))
            for label in form.get("labels", []):
                self.assertIn(label, self.labels, path.name)
            ids = [field["id"] for field in form.get("body", []) if "id" in field]
            self.assertEqual(len(ids), len(set(ids)), path.name)

    def test_registration_does_not_claim_qualification_or_require_synced_host(self):
        self.assertIn("registration", self.form["name"].lower())
        self.assertNotRegex(str(self.form).lower(), r"\b(applications?|applicants?|apply|applying)\b")
        applied = set(self.form["labels"])
        self.assertTrue(
            {"type:registration", "intake:operator", "status:intake"} <= applied
        )
        self.assertFalse(
            applied
            & {"intake:sync-qualified", "intake:rpc-active", "intake:validator-active"}
        )
        self.assertEqual(self.fields["team"]["validations"]["required"], "true")
        self.assertEqual(self.fields["evidence"]["validations"]["required"], "false")
        self.assertEqual(self.fields["rpc"]["validations"]["required"], "false")
        self.assertIn(
            "planning a host", self.fields["preparation"]["attributes"]["options"]
        )
        self.assertEqual(
            self.fields["network"]["attributes"]["options"], ["devnet", "testnet"]
        )
        self.assertEqual(len(self.fields["role"]["attributes"]["options"]), 3)
        self.assertTrue(
            all(
                item["required"] == "true"
                for item in self.fields["acknowledgments"]["attributes"]["options"]
            )
        )

    def test_rpc_pool_details_are_private_and_public_evidence_is_optional(self):
        rpc = self.fields["rpc"]
        self.assertEqual(rpc["validations"]["required"], "false")
        description = rpc["attributes"]["description"]
        self.assertIn(
            "Share the dedicated RPC origin hostname, fixed IP and incident contacts privately",
            description,
        )
        self.assertNotRegex(rpc["attributes"]["placeholder"], r"(?i)hostname|ipv4|fixed ip")
        evidence = self.fields["evidence"]
        self.assertEqual(evidence["validations"]["required"], "false")
        self.assertIn("public P2P multiaddress", evidence["attributes"]["placeholder"])
        self.assertIn("restart attestation separately", evidence["attributes"]["description"])

    def test_intake_is_protected_while_other_needs_info_issues_still_expire(self):
        config = load(".github/workflows/stale.yml")["jobs"]["stale"]["steps"][0][
            "with"
        ]
        self.assertEqual(config["only-labels"], "status:needs-info")
        exemptions = set(config["exempt-issue-labels"].split(","))
        self.assertIn("intake:operator", exemptions)
        self.assertEqual(config["days-before-issue-stale"], "14")
        self.assertEqual(config["days-before-issue-close"], "7")
        # The pinned shared triage action protects every non-triage status label.
        self.assertTrue(
            any(
                re.match(r"^status:(?!triage$)", label) for label in self.form["labels"]
            )
        )

    def test_public_routes_and_documented_intake_labels_exist(self):
        for name in ["README.md", "SUPPORT.md", "OPERATOR-INTAKE.md"]:
            self.assertIn(
                "template=operator-application.yml", (ROOT / name).read_text()
            )
        for label in re.findall(
            r"`((?:intake|status|role|net|type):[^`]+)`",
            (ROOT / "OPERATOR-INTAKE.md").read_text(),
        ):
            self.assertIn(label, self.labels)

    def test_model_sponsorship_routes_to_testnet_intake(self):
        template = "model-upload-sponsorship.yml"
        form = load(f".github/ISSUE_TEMPLATE/{template}")
        applied = set(form["labels"])
        self.assertEqual(
            {label for label in applied if label.startswith("net:")}, {"net:testnet"}
        )
        self.assertTrue({"status:intake", "intake:model-upload"} <= applied)
        self.assertNotIn("intake:operator", applied)
        for name in ["README.md", "SUPPORT.md"]:
            self.assertIn(f"template={template}", (ROOT / name).read_text())

    def test_duplicate_yaml_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            yaml.load("labels: [a]\nlabels: [b]\n", Loader=UniqueLoader)
        for path in (ROOT / ".github/workflows").glob("*.yml"):
            load(path.relative_to(ROOT))


if __name__ == "__main__":
    unittest.main()
