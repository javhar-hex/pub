import base64
import dataclasses as dc
import io
import json
import os
from typing import Optional

import pandas as pd
import requests


@dc.dataclass(frozen=True)
class GitHubIo:
    pat: str
    owner: str
    repo: str
    branch: str
    folder: Optional[str] = None

    def upload(
            self,
            df: pd.DataFrame,
            filename: str,
            folder: Optional[str] = None,
            include_index: bool = False,
            message: str = "Add/Update CSV from notebook",
    ) -> requests.Response:
        csv_bytes = df.to_csv(index=include_index).encode("utf-8")

        headers = self._headers(pat=self.pat, use_json=True)

        url = self._url(filename, folder)

        response = requests.get(url, headers=headers, params={"ref": self.branch})
        sha = response.json().get("sha") if response.status_code == 200 else None

        payload = {
            "message": message,
            "content": base64.b64encode(csv_bytes).decode("ascii"),
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha

        try:
            response = requests.put(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response
        except requests.HTTPError:
            print("Status:", response.status_code)
            print("Reason:", response.reason)
            print("Body:", response.text)
            raise

    def download(
            self,
            filename: str,
            folder: Optional[str] = None,
            index_col: Optional[int] = None,
    ) -> pd.DataFrame:
        headers = self._headers(pat=self.pat, use_json=False)

        url = self._url(filename, folder)
        resp = requests.get(url, headers=headers, params={"ref": self.branch}, timeout=30)
        resp.raise_for_status()  # will throw if 401/403/etc.

        df: pd.DataFrame = pd.read_csv(io.BytesIO(resp.content), index_col=index_col)
        return df

    def _url(self, filename: str, folder: Optional[str]) -> str:
        if folder is None:
            folder = self.folder
        if folder is None:
            raise ValueError("No folder specified.")
        path = os.path.join(folder, filename)
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{path}"

    def _headers(self, pat: str, use_json: bool) -> dict[str, str]:
        suffix = "+json" if use_json else ".v3.raw"
        return {
            "Authorization": f"Bearer {pat}",
            "Accept": f"application/vnd.github{suffix}",
        }
