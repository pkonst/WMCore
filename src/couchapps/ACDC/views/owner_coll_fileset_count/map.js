function(doc) {
  var count = 0;
  for (var file in doc.files) {
    if (doc.files.hasOwnProperty(file)) {
      count += 1;
    }
  }
  emit([doc.owner.group, doc.owner.user, doc.collection_name, doc.fileset_name], count);
}