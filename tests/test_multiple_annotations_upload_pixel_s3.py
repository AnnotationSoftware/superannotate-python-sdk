from pathlib import Path
from urllib.parse import urlparse

import pytest

import superannotate as sa
sa.init(Path.home() / ".annotateonline" / "config.json")

TEST_PROJECT_PIXEL = "sample_project_pixel"
TEST_PROJECT_VECTOR = "sample_project_vector"


@pytest.fixture
def empty_test_project():
    team = sa.get_default_team()

    projects_found = sa.search_projects(team, "test_upload_41")
    for pr in projects_found:
        sa.delete_project(pr)


def test_upload_from_s3(empty_test_project, tmpdir):
    team = sa.get_default_team()
    project = sa.create_project(
        team, "test_upload_41", "hk_test", project_type=2
    )

    f = urlparse(f"s3://hovnatan-test/{TEST_PROJECT_PIXEL}")
    sa.upload_images_from_folder(
        project, f.path[1:], annotation_status=1, from_s3_bucket=f.netloc
    )
    old_to_new_classes_conversion = sa.create_classes_from_classes_json(
        project, f.path[1:] + '/classes/classes.json', from_s3_bucket=f.netloc
    )
    assert sa.get_project_image_count(project) == 6

    sa.upload_annotations_from_folder(
        project,
        TEST_PROJECT_PIXEL,
        old_to_new_classes_conversion,
        from_s3_bucket=f.netloc
    )

    for image in sa.search_images(project):
        sa.download_image_annotations(image, tmpdir)

    assert len(list(Path(tmpdir).glob("*.*"))) == 8
    sa.delete_project(project)


def test_pixel_preannotation_upload_from_s3(empty_test_project, tmpdir):
    team = sa.get_default_team()
    project = sa.create_project(
        team, "test_upload_41", "hk_test", project_type=2
    )

    f = urlparse(f"s3://hovnatan-test/{TEST_PROJECT_PIXEL}")
    sa.upload_images_from_folder(
        project, f.path[1:], annotation_status=1, from_s3_bucket=f.netloc
    )
    old_to_new_classes_conversion = sa.create_classes_from_classes_json(
        project, f.path[1:] + '/classes/classes.json', from_s3_bucket=f.netloc
    )
    assert sa.get_project_image_count(project) == 6

    sa.upload_preannotations_from_folder(
        project,
        TEST_PROJECT_PIXEL,
        old_to_new_classes_conversion,
        from_s3_bucket=f.netloc
    )

    for image in sa.search_images(project):
        sa.download_image_preannotations(image, tmpdir)

    assert len(list(Path(tmpdir).glob("*.*"))) == 0
    sa.delete_project(project)


def test_vector_preannotation_upload_from_s3(empty_test_project, tmpdir):
    team = sa.get_default_team()
    project = sa.create_project(
        team, "test_upload_41", "hk_test", project_type=1
    )

    f = urlparse(f"s3://hovnatan-test/{TEST_PROJECT_VECTOR}")
    sa.upload_images_from_folder(
        project, f.path[1:], annotation_status=1, from_s3_bucket=f.netloc
    )
    old_to_new_classes_conversion = sa.create_classes_from_classes_json(
        project, f.path[1:] + '/classes/classes.json', from_s3_bucket=f.netloc
    )
    assert sa.get_project_image_count(project) == 6

    sa.upload_preannotations_from_folder(
        project,
        TEST_PROJECT_VECTOR,
        old_to_new_classes_conversion,
        from_s3_bucket=f.netloc
    )

    for image in sa.search_images(project):
        sa.download_image_preannotations(image, tmpdir)

    assert len(list(Path(tmpdir).glob("*.*"))) == 6
    sa.delete_project(project)