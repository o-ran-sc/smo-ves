.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

smo/ves Overview
================

This project supports the O1/VES interface in SMO. It consists of several components

- A VES collector that is a collector of events posted by different Network Functions (NF) of the RAN
- Kafka Bus which acts as the message bus in SMO
- A connector to connect the Kafka Bus to a Grafana dashboard
- A connector to connect the Kafka Bus to InfluxdB to persist all the data posted on the Kafka Bus
- A connector that provides an adapter for applications that want to read the Kafka events as DMaaP events.
