from pathlib import Path

from datamodel_code_generator import (
    DataModelType,
    InputFileType,
    generate,
)
from datamodel_code_generator.format import (
    PythonVersion,
)

if __name__ == "__main__":
    generate(
        input_=Path(
            "/Users/josephcourtney/Dropbox/code/Python/uncategorized/chiaro/bg/datamodel-code-generator/schema.json"
        ),
        input_file_type=InputFileType.JsonSchema,
        output=Path(
            "/Users/josephcourtney/Dropbox/code/Python/uncategorized/chiaro/bg/datamodel-code-generator/model.py"
        ),
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_312,
    )
