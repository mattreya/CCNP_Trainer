import unittest
import os
import shutil
import json
from unittest.mock import patch, MagicMock, mock_open
from slash_commands import quiz_me, generate_gns3_config, get_question_bank_path
import random

class TestQuizMe(unittest.TestCase):
    def tearDown(self):
        # Clean up gns3_configs directory after each test
        if os.path.exists("gns3_configs"):
            shutil.rmtree("gns3_configs")
        # Clean up question_bank directory after each test
        if os.path.exists("question_bank"):
            shutil.rmtree("question_bank")

    def setUp(self):
        # Create dummy directories
        os.makedirs("question_bank/infrastructure", exist_ok=True)

    @patch('slash_commands.random.sample')
    @patch('builtins.input', side_effect=['C', 'A', 'A'])
    def test_quiz_me_pass(self, mock_input, mock_random_sample):
        mock_question_bank_content = json.dumps([
            {"question": "What is the default administrative distance of OSPF?", "options": {"A": "90", "B": "100", "C": "110", "D": "120"}, "answer": "C"},
            {"question": "Which command is used to enable OSPF on a router?", "options": {"A": "router ospf <process-id>", "B": "enable ospf", "C": "ip ospf enable", "D": "ospf run"}, "answer": "A"},
            {"question": "What is the multicast address used by OSPF?", "options": {"A": "224.0.0.5", "B": "224.0.0.9", "C": "224.0.0.10", "D": "224.0.0.1"}, "answer": "A"}
        ])
        
        question_bank_path = get_question_bank_path("OSPF")
        with open(question_bank_path, "w") as f:
            f.write(mock_question_bank_content)

        mock_random_sample.return_value = json.loads(mock_question_bank_content)

        result = quiz_me('multiple choice', 'OSPF', num_questions=3)
        self.assertIn("You scored 100.00%", result)

    @patch('slash_commands.random.sample')
    @patch('builtins.input', side_effect=['A', 'B', 'C'])
    def test_quiz_me_fail(self, mock_input, mock_random_sample):
        mock_question_bank_content = json.dumps([
            {"question": "What is the default administrative distance of OSPF?", "options": {"A": "90", "B": "100", "C": "110", "D": "120"}, "answer": "C"},
            {"question": "Which command is used to enable OSPF on a router?", "options": {"A": "router ospf <process-id>", "B": "enable ospf", "C": "ip ospf enable", "D": "ospf run"}, "answer": "A"},
            {"question": "What is the multicast address used by OSPF?", "options": {"A": "224.0.0.5", "B": "224.0.0.9", "C": "224.0.0.10", "D": "224.0.0.1"}, "answer": "A"}
        ])
        
        question_bank_path = get_question_bank_path("OSPF")
        with open(question_bank_path, "w") as f:
            f.write(mock_question_bank_content)

        mock_random_sample.return_value = json.loads(mock_question_bank_content)

        result = quiz_me('multiple choice', 'OSPF', num_questions=3)
        self.assertIn("You scored 0.00%. You answered 0 out of 3 questions correctly.", result)

    @patch('slash_commands.generate_questions')
    @patch('slash_commands.random.sample')
    @patch('builtins.input', side_effect=['Z', 'Z', 'Z', 'Z', 'Z', 'Z'])
    def test_quiz_me_gns3_trigger(self, mock_input, mock_random_sample, mock_generate_questions):
        original_ospf_questions = [
            {"question": "What is the default administrative distance of OSPF?", "options": {"A": "90", "B": "100", "C": "110", "D": "120"}, "answer": "C"},
        ]
        dummy_questions = [
            {"question": "Dummy Q2", "options": {"A": "a", "B": "b"}, "answer": "B"},
            {"question": "Dummy Q3", "options": {"A": "a", "B": "b"}, "answer": "B"},
            {"question": "Dummy Q4", "options": {"A": "a", "B": "b"}, "answer": "B"},
            {"question": "Dummy Q5", "options": {"A": "a", "B": "b"}, "answer": "B"},
            {"question": "Dummy Q6", "options": {"A": "a", "B": "b"}, "answer": "B"}
        ]
        
        question_bank_path = get_question_bank_path("OSPF")
        with open(question_bank_path, "w") as f:
            json.dump(original_ospf_questions, f)
            
        mock_generate_questions.return_value = dummy_questions
        mock_random_sample.return_value = original_ospf_questions + dummy_questions

        # Mock gns3_topology.json
        mock_topology_content = json.dumps({
            "routers": [
                {"name": "R1", "interfaces": [{"name": "GigabitEthernet0/0", "ip_address": "10.0.0.1", "subnet_mask": "255.255.255.252"}]},
                {"name": "R2", "interfaces": [{"name": "GigabitEthernet0/0", "ip_address": "10.0.0.2", "subnet_mask": "255.255.255.252"}]}
            ],
            "links": [
                {"device1": "R1", "interface1": "GigabitEthernet0/0", "device2": "R2", "interface2": "GigabitEthernet0/0"}
            ]
        })
        with open("gns3_topology.json", "w") as f:
            f.write(mock_topology_content)

        result = quiz_me('multiple choice', 'OSPF', num_questions=6)
        self.assertIn("GNS3 configuration files have been generated", result)

    def test_generate_gns3_config(self):
        mock_topology_content = json.dumps({
            "routers": [
                {"name": "R1", "interfaces": [{"name": "GigabitEthernet0/0", "ip_address": "10.0.0.1", "subnet_mask": "255.255.255.252"}]},
                {"name": "R2", "interfaces": [{"name": "GigabitEthernet0/0", "ip_address": "10.0.0.2", "subnet_mask": "255.255.255.252"}]}
            ],
            "links": [
                {"device1": "R1", "interface1": "GigabitEthernet0/0", "device2": "R2", "interface2": "GigabitEthernet0/0"}
            ]
        })
        with open("gns3_topology.json", "w") as f:
            f.write(mock_topology_content)

        result = generate_gns3_config("OSPF")
        self.assertEqual(result, "GNS3 configuration files have been generated in the 'gns3_configs' directory.")
        self.assertTrue(os.path.exists("gns3_configs"))
        self.assertTrue(os.path.exists("gns3_configs/R1_config.txt"))
        self.assertTrue(os.path.exists("gns3_configs/R2_config.txt"))

if __name__ == '__main__':
    unittest.main()