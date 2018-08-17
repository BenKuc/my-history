# TODO: make this extensible: let user define signal-classes and model-methods that should be tracked

# TODO: existing signals:
# Deletion for single instance and qs -> post_delete;
# Creation/Update for single instance -> post_save;
# Creation of multiple instances -> custom: post_bulk_create; + custom: post_custom_bulk_create;
# Update of multiple instances -> custom: post_update;
