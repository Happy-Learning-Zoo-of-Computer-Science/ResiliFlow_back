from marshmallow import Schema, fields


class PipelineExecuteRequest(Schema):
    pipeline_name = fields.String(required=True)
    yaml_path = fields.String(required=True)
