#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <boost/log/trivial.hpp>
#include <boost/log/sources/global_logger_storage.hpp>
#include <boost/log/sources/severity_feature.hpp>
#include <boost/log/sinks/syslog_backend.hpp>

namespace Pr
{
/**
 * \brief Class providing uniform access to send messages to log
 */
class Logger
{
public:
    /**
     * \brief Enum defining different types of log messages
     */
    enum LogMessageType
    {
        Warning, Error, Info
    };

    /**
     * \brief Send message to log.
     *
     * \param type                      Message type.
     * \param message                   Message text.
     */
    static void log(LogMessageType type, const std::string& message);

    static void init(const std::string& name);

    static char name[255];

    static void flush();
};

}

BOOST_LOG_INLINE_GLOBAL_LOGGER_DEFAULT(my_logger, boost::log::sources::severity_logger_mt<boost::log::sinks::syslog::level>)

#define PROCESS_LOG(lvl)\
    BOOST_LOG_SEV(my_logger::get(), boost::log::sinks::syslog::lvl) << Pr::Logger::name << ":PRCSS "

#endif
