project(generate_queries)
cmake_minimum_required(VERSION 2.8)

set(REQUIRED_LIBRARIES
                boost_program_options
                boost_filesystem
                boost_date_time
                boost_thread
                boost_python-py34
                boost_system
                boost_log
                boost_timer
)

aux_source_directory(. SRC_LIST)
add_executable(${PROJECT_NAME} ${SRC_LIST})


find_package(PkgConfig)
pkg_check_modules(GTK "gtkmm-3.0")
target_link_libraries(${PROJECT_NAME}  ${GTK_LIBRARIES})
add_definitions(${GTK_CFLAGS} ${GTK_CFLAGS_OTHER})

pkg_check_modules(WK "webkit2gtk-3.0")
target_link_libraries(${PROJECT_NAME}  ${WK_LIBRARIES})
add_definitions(${WK_CFLAGS} ${WK_CFLAGS_OTHER})



target_link_libraries(${PROJECT_NAME} ${REQUIRED_LIBRARIES})
