# forward_observation.assert_has_calls(
#    [
#        call.add_field("messageId", "123"),
#        call.add_field("sender", "mesh123"),
#        call.add_field("recipient", "mesh456"),
#        call.add_field("fileName", "a_file.dat"),
#        call.finish(),
#    ],
#    any_order=False,
# )

# observation.assert_has_calls(
#    [
#        call.add_field("messageId", "abc"),
#        call.add_field("sender", "mesh123"),
#        call.add_field("recipient", "mesh456"),
#        call.add_field("fileName", "a_file.dat"),
#        call.add_field("error", MISSING_MESH_HEADER_ERROR),
#        call.add_field("missingHeaderName", "fruit_header"),
#        call.finish(),
#    ],
#    any_order=False,
# )
